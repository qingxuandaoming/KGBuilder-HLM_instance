<template>
  <div class="kgqa-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>红楼梦人物关系问答系统</span>
      </div>
      <div class="search-box">
        <el-input
          v-model="query"
          placeholder="请输入你的问题(eg.贾宝玉的爸爸是谁？)"
          class="input-with-select"
          @keyup.enter.native="handleSearch"
        >
          <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
        </el-input>
      </div>
      
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="16">
          <div id="graph-container" style="height: 600px; border: 1px solid #eee;"></div>
        </el-col>
        <el-col :span="8">
          <el-card v-if="profile" class="profile-card">
            <div slot="header">
              <span>{{ profile.name }}</span>
            </div>
            <!-- Profile content is raw HTML from backend -->
            <div class="profile-content" v-html="profile.content"></div>
            <div v-if="profile.image" class="profile-image" style="margin-top: 10px; text-align: center;">
               <img :src="'data:image/jpg;base64,' + profile.image" style="max-width: 100%; max-height: 300px;" />
            </div>
          </el-card>
          <div v-else class="empty-profile">
            <el-alert
              title="提示"
              type="info"
              description="点击图谱中的节点查看详细人物百科"
              show-icon
              :closable="false">
            </el-alert>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: "KGQA",
  data() {
    return {
      query: "",
      chart: null,
      profile: null,
      pythonApiUrl: "http://localhost:5000", // Python backend URL
      categories: ["贾家荣国府", "贾家宁国府", "王家", "史家", "薛家", "其他", "林家"]
    };
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById('graph-container'));
      this.chart.on('click', (params) => {
        if (params.dataType === 'node') {
          this.getProfile(params.name);
        }
      });
      // Render empty or initial graph
      this.renderGraph({nodes: [], links: []}); 
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    async handleSearch() {
      if (!this.query) return;
      
      this.chart.showLoading();
      try {
        const response = await axios.get(`${this.pythonApiUrl}/KGQA_answer`, {
          params: { name: this.query }
        });
        
        // Response format from Python: [{data: [...], links: [...], meta: {...}}]
        // Check if response is array and has data
        if (!response.data || response.data.length === 0) {
            this.$message.warning("未找到相关结果");
            return;
        }

        const result = response.data[0];
        
        if (result.meta && result.meta.message) {
           if (!result.data || result.data.length === 0) {
             let msg = result.meta.message;
             if (result.meta.candidates && result.meta.candidates.length > 0) {
                 msg += "\n猜你想问：" + result.meta.candidates.join(", ");
             }
             this.$alert(msg, '提示', { confirmButtonText: '确定' });
             return;
           }
        }

        this.renderGraph({
          nodes: result.data,
          links: result.links
        });
        
      } catch (error) {
        console.error("Search failed:", error);
        this.$message.error("搜索失败，请检查Python后端服务是否启动 (端口5000)");
      } finally {
        this.chart.hideLoading();
      }
    },
    renderGraph(data) {
      const option = {
        title: { text: '' },
        tooltip: {
           formatter: function (node) {
               if (node.dataType === 'edge') return node.data.relation || node.name;
               return node.data.name;
           }
        },
        legend: {
           data: this.categories,
           x: "center"
        },
        series: [{
          type: 'graph',
          layout: 'force',
          symbolSize: 50,
          roam: true,
          label: { 
              show: true,
              fontSize: 12
          },
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [4, 10],
          edgeLabel: {
            fontSize: 10,
            show: true,
            formatter: "{c}" // Displays the value (relation)
          },
          force: {
            repulsion: 1000,
            edgeLength: [50, 200]
          },
          draggable: true,
          categories: this.categories.map(name => ({ name })),
          data: data.nodes.map((node, idx) => ({
            ...node,
            id: String(idx), 
            name: node.name,
            // If backend sends category index, echarts uses it. 
            // If backend sends category name, we might need to map. 
            // Assuming backend sends compatible data structure as in original project.
          })),
          links: data.links
        }]
      };
      
      this.chart.setOption(option);
    },
    async getProfile(name) {
      try {
        const response = await axios.get(`${this.pythonApiUrl}/get_profile`, {
           params: { character_name: name }
        });
        // Response: [html_content, base64_image_string]
        const data = response.data;
        if (data && data.length >= 2) {
            this.profile = {
            name: name,
            content: data[0],
            image: data[1]
            };
        } else {
            this.profile = { name: name, content: "暂无详细资料", image: null };
        }
      } catch (error) {
        console.error("Get profile failed:", error);
        this.$message.error("获取人物资料失败");
      }
    }
  }
};
</script>

<style scoped>
.kgqa-container {
  padding: 20px;
}
.profile-content {
  font-size: 14px;
  line-height: 1.6;
  max-height: 500px;
  overflow-y: auto;
}
.empty-profile {
    padding: 20px;
    text-align: center;
    color: #999;
}
</style>
