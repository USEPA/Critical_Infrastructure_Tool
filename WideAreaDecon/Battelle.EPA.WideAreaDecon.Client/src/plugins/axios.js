import Vue from 'vue';
import axios from 'axios';

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const config = {
  // baseURL: process.env.baseURL || process.env.apiUrl || ""
  timeout: 30 * 1000, // Timeout
  // withCredentials: true, // Check cross-site Access-Control
};

const createdAxios = axios.create(config);

createdAxios.interceptors.request.use(
  function requestInterceptorAction() {
    // Do something before request is sent
    return config;
  },
  function requestErrorAction(error) {
    // Do something with request error
    return Promise.reject(error);
  },
);

// Add a response interceptor
createdAxios.interceptors.response.use(
  function responseInterceptorAction(response) {
    // Do something with response data
    return response;
  },
  function responseErrorAction(error) {
    // Do something with response error
    return Promise.reject(error);
  },
);

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
Plugin.install = function installAxiosPlugin(vueInstance) {
  // eslint-disable-next-line no-param-reassign
  vueInstance.axios = createdAxios;
  window.axios = createdAxios;
  Object.defineProperties(vueInstance.prototype, {
    axios: {
      // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
      get() {
        return createdAxios;
      },
    },
    $axios: {
      // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
      get() {
        return createdAxios;
      },
    },
  });
};

Vue.use(Plugin);

export default Plugin;
