import axios from 'axios';

// Load base URL from environment variables or default to localhost:5000
const BASE_URL = process.env.VUE_APP_KGQA_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

export default {
  /**
   * Get answer from KGQA system
   * @param {string} name - The question or entity name
   * @returns {Promise}
   */
  getAnswer(name) {
    return apiClient.get('/KGQA_answer', {
      params: { name }
    });
  },

  /**
   * Get profile for a character
   * @param {string} characterName 
   * @returns {Promise}
   */
  getProfile(characterName) {
    return apiClient.get('/get_profile', {
      params: { character_name: characterName }
    });
  },

  /**
   * Search for relations of a name
   * @param {string} name 
   * @returns {Promise}
   */
  searchName(name) {
    return apiClient.get('/search_name', {
      params: { name }
    });
  }
};
