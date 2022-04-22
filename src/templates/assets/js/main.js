window.$ = window.jQuery = require("jquery");
import "startbootstrap-sb-admin-2/js/sb-admin-2";
import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import Select2 from "v-select2-component";
import Toasted from "vue-toasted";

// Import Bootstrap and BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "../scss/main.scss";

window.Vue = Vue;

Vue.use(Toasted, {
  class: "rounded",
  position: "bottom-right",
  fitToScreen: true,
  theme: "toasted-primary",
  duration: 4000,
});
// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
Vue.component("Select2", Select2);

Vue.component(
  "create-product",
  require("./components/product/CreateProduct.vue").default
);
Vue.component(
  "list-product",
  require("./components/product/ListProduct.vue").default
);

Vue.component(
  "update-product",
  require("./components/product/UpdateProduct.vue").default
);

const main = new Vue({
  el: "#app",
});
