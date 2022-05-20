<template>
  <section>
    <div class="row">
      <div class="col-md-6">
        <div class="card shadow mb-4">
          <div class="card-body">
            <div class="form-group">
              <label for="">Product Name</label>
              <input
                type="text"
                v-model="product_name"
                placeholder="Product Name"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="">Product SKU</label>
              <input
                type="text"
                v-model="product_sku"
                placeholder="Product Name"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="">Description</label>
              <textarea
                v-model="description"
                id=""
                cols="30"
                rows="4"
                class="form-control"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="card shadow mb-4">
          <div
            class="card-header py-3 d-flex flex-row align-items-center justify-content-between"
          >
            <h6 class="m-0 font-weight-bold text-primary">Media</h6>
          </div>
          <div class="card-body border">
            <vue-dropzone
              ref="myVueDropzone"
              id="dropzone"
              :options="dropzoneOptions"
            ></vue-dropzone>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow mb-4">
          <div
            class="card-header py-3 d-flex flex-row align-items-center justify-content-between"
          >
            <h6 class="m-0 font-weight-bold text-primary">Variants</h6>
          </div>
          <div class="card-body">
            <div
              class="row"
              v-for="(item, index) in product_variant"
              :key="index"
            >
              <div class="col-md-4">
                <div class="form-group">
                  <label for="">Option</label>
                  <select v-model="item.option" class="form-control">
                    <option
                      v-for="variant in variants"
                      :value="variant.id"
                      :key="variant.id"
                    >
                      {{ variant.title }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-8">
                <div class="form-group">
                  <label
                    v-if="product_variant.length != 1"
                    @click="
                      product_variant.splice(index, 1);
                      checkVariant;
                    "
                    class="float-right text-primary"
                    style="cursor: pointer"
                    >Remove</label
                  >
                  <label v-else for="">.</label>
                  <input-tag
                    v-model="item.tags"
                    @input="checkVariant"
                    class="form-control"
                  ></input-tag>
                </div>
              </div>
            </div>
          </div>
          <div
            class="card-footer"
            v-if="
              product_variant.length < variants.length &&
              product_variant.length < 3
            "
          >
            <button @click="newVariant" class="btn btn-primary">
              Add another option
            </button>
          </div>

          <div class="card-header text-uppercase">Preview</div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <td>Variant</td>
                    <td>Price</td>
                    <td>Stock</td>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="variant_price in product_variant_prices"
                    :key="variant_price.id"
                  >
                    <td>{{ variant_price.title }}</td>
                    <td>
                      <input
                        type="text"
                        class="form-control"
                        v-model="variant_price.price"
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        class="form-control"
                        v-model="variant_price.stock"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button @click="saveProduct" type="submit" class="btn btn-lg btn-primary">
      Save
    </button>
    <button type="button" class="btn btn-secondary btn-lg">Cancel</button>
  </section>
</template>

<script>
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
import InputTag from "vue-input-tag";

import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/",
});

export default {
  components: {
    vueDropzone: vue2Dropzone,
    InputTag,
  },
  props: {
    variants: {
      type: Array,
      required: true,
    },
    selectedProductId: {
      required: true,
    },
  },
  data() {
    return {
      productApiUrl: "api/v1/product/products/",
      selectedProduct: null,
      product_name: "",
      product_sku: "",
      description: "",
      images: [],
      product_variant: [
        {
          option: this.variants[0].id,
          tags: [],
        },
      ],
      product_variant_prices: [],
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: { "My-Awesome-Header": "header value" },
      },
    };
  },
  created() {
    this.getSelectedProductDetail();
  },

  methods: {
    getSelectedProductDetail() {
      let relativeURL = this.productApiUrl + this.selectedProductId + "/";
      apiClient
        .get(relativeURL)
        .then((resp) => {
          this.selectedProduct = resp.data;
          this.setProductData();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    setProductPriceVarinat() {
      let productPriceVariants = JSON.parse(
        JSON.stringify(this.selectedProduct.productvariantprices_display)
      );
      productPriceVariants.forEach((element) => {
        console.log(element);
        let price_title = "";
        if (element.product_variant_one_display.variant_title) {
          price_title = `${price_title}/${element.product_variant_one_display.variant_title}`;
        }
        if (element.product_variant_two_display.variant_title) {
          price_title = `${price_title}/${element.product_variant_two_display.variant_title}`;
        }
        if (element.product_variant_three_display.variant_title) {
          price_title = `${price_title}/${element.product_variant_three_display.variant_title}`;
        }

        this.product_variant_prices.push({
          title: price_title,
          price: element.price,
          stock: element.stock,
        });
      });
    },

    setProductData() {
      if (this.selectedProduct) {
        this.product_name = this.selectedProduct.title;
        this.product_sku = this.selectedProduct.sku;
        this.description = this.selectedProduct.description;

        this.setProductVarinat();
        this.setProductPriceVarinat();
      }
    },

    setProductSize(productvariant) {
      this.product_variant.forEach((element) => {
        if (element.option == this.variants[0].id) {
          element.tags.push(productvariant.variant_title);
        }
      });
    },
    setProductColor(productvariant) {
      this.product_variant.forEach((element) => {
        if (element.option == this.variants[1].id) {
          element.tags.push(productvariant.variant_title);
        }
      });
    },
    setProductStyle(productvariant) {
      this.product_variant.forEach((element) => {
        if (element.option == this.variants[2].id) {
          element.tags.push(productvariant.variant_title);
        }
      });
    },

    setProductVarinat() {
      let productVariants = JSON.parse(
        JSON.stringify(this.selectedProduct.productvariants_display)
      );

      if (productVariants) {
        productVariants.forEach((element) => {
          let is_variant_exist = this.checkIsVariantExists(element);

          if (this.variants[0].id == element.variant) {
            if (!is_variant_exist) {
              this.product_variant.push({
                option: this.variants[element.variant].id,
                tags: [],
              });
            }
            this.setProductSize(element);
          } else if (this.variants[1].id == element.variant) {
            if (!is_variant_exist) {
              this.product_variant.push({
                option: this.variants[1].id,
                tags: [],
              });
            }
            this.setProductColor(element);
          } else if (this.variants[2].id == element.variant) {
            if (!is_variant_exist) {
              this.product_variant.push({
                option: this.variants[2].id,
                tags: [],
              });
            }
            this.setProductStyle(element);
          }
        });
      }
    },

    checkIsVariantExists(p_variant) {
      let isFound = false;
      this.product_variant.forEach((element) => {
        if (element.option == p_variant.variant) {
          isFound = true;
        }
      });
      return isFound;
    },

    // it will push a new object into product variant
    newVariant() {
      let all_variants = this.variants.map((el) => el.id);
      let selected_variants = this.product_variant.map((el) => el.option);
      let available_variants = all_variants.filter(
        (entry1) => !selected_variants.some((entry2) => entry1 == entry2)
      );

      this.product_variant.push({
        option: available_variants[0],
        tags: [],
      });
    },

    // check the variant and render all the combination
    checkVariant() {
      let tags = [];
      this.product_variant_prices = [];
      this.product_variant.filter((item) => {
        tags.push(item.tags);
      });

      this.getCombn(tags).forEach((item) => {
        this.product_variant_prices.push({
          title: item,
          price: 0,
          stock: 0,
        });
      });
    },

    // combination algorithm
    getCombn(arr, pre) {
      pre = pre || "";
      if (!arr.length) {
        return pre;
      }
      let self = this;
      let ans = arr[0].reduce(function (ans, value) {
        return ans.concat(self.getCombn(arr.slice(1), pre + value + "/"));
      }, []);
      return ans;
    },

    convertToSlug(text) {
      return text
        .toLowerCase()
        .replace(/ /g, "-")
        .replace(/[^\w-]+/g, "");
    },

    // store product into database
    saveProduct() {
      let product = {
        title: this.product_name,
        sku: this.convertToSlug(this.product_sku),
        description: this.description,
        product_image: this.images,
        product_variant: this.product_variant,
        product_variant_prices: this.product_variant_prices,
      };

      let relativeURL = this.productApiUrl + this.selectedProductId + "/";
      apiClient
        .patch(relativeURL, product)
        .then((resp) => {
          console.log(resp);
          Vue.toasted.show("Product Updated successfully", {
            className: "bg-success",
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    console.log("Component mounted.");
  },
};
</script>
