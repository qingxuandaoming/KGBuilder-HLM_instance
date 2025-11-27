<template>
  <div id="follow-us" class="guanzhu" style="padding: 20px;">
    <h2 class="hometitle">关于项目</h2>
    <ul>
      <li class="wx" style="text-align: center;">
        <a target="_blank" href="https://github.com/MiracleTanC/Neo4j-KGBuilder.git" style="text-decoration: none; color: #409EFF; font-weight: bold;">
           访问 GitHub 仓库
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    data: Object
  },
  data() {
    return {

    };
  },
  mounted() {},
  components: {},
  methods: {

  }
};
</script>
<style>
.guanzhu ul li {
  font-size: 14px;
  margin-bottom: 10px;
  background: #fff;
  color: #525252;
  line-height: 40px;
  border: 1px solid #ddd;
  border-radius: 2px;
  position: relative;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>
