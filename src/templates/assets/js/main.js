window.$ = window.jQuery = require("jquery");
import "startbootstrap-sb-admin-2/js/sb-admin-2";
import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
// Import Bootstrap and BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "../scss/main.scss";

window.Vue = Vue;

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

Vue.component(
  "create-product",
  require("./components/product/CreateProduct.vue").default
);
Vue.component(
  "list-product",
  require("./components/product/ListProduct.vue").default
);

const main = new Vue({
  el: "#app",
});
