<template>
  <div class="card">
    <div class="card-header">
      <div class="form-row justify-content-between">
        <div class="col-md-2">
          <input
            type="text"
            name="title"
            placeholder="Product Title"
            class="form-control"
            v-model="search_query"
          />
        </div>
        <div class="col-md-2">
          <b-form-select
            v-model="filter_settings.variant"
            :options="getVariantOptions"
            size="sm"
            class=""
          >
          </b-form-select>
        </div>

        <div class="col-md-3">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text">Price Range</span>
            </div>
            <input
              type="text"
              name="price_from"
              aria-label="First name"
              placeholder="From"
              class="form-control"
              v-model="filter_settings.from_price_range"
            />
            <input
              type="text"
              name="price_to"
              aria-label="Last name"
              placeholder="To"
              class="form-control"
              v-model="filter_settings.to_price_range"
            />
          </div>
        </div>
        <div class="col-md-2">
          <input
            type="date"
            name="date"
            placeholder="Date"
            class="form-control"
            v-model="filter_settings.createdDate"
          />
        </div>
        <div class="col-md-1">
          <b-button
            v-if="isFiltersApplied"
            title="Clear filter"
            class="btn btn-primary float-right ml-2"
            @click="clearFilter()"
            variant="danger"
          >
            <i class="fa fa-times-circle"></i>
          </b-button>

          <button
            @click="fetchProductList(1), (isFiltersApplied = true)"
            class="btn btn-primary float-right mr-2"
          >
            <i class="fa fa-search"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="card-body">
      <div class="table-response">
        <table class="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Title</th>
              <th>Description</th>
              <th>Variant</th>
              <th width="150px">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(product, product_index) in productList"
              :key="product_index"
            >
              <td>{{ product_index + 1 }}</td>
              <td>
                {{ product.title }} <br />
                <!-- Created at : 25-Aug-2020 -->
                Created at : {{ product.created_at }}
              </td>
              <td>{{ product.description }}</td>
              <td>
                <dl
                  class="row mb-0"
                  style="height: 80px; overflow: hidden"
                  id="variant"
                  v-for="(
                    varint, varint_index
                  ) in product.productvariantprices_display"
                  :key="varint_index"
                >
                  <!-- {{ varint }} -->

                  <dt class="col-sm-3 pb-0">
                    <template v-if="varint.product_variant_one_display">
                      {{ varint.product_variant_one_display.variant_title }}/
                    </template>
                    <template v-if="varint.product_variant_two_display">
                      {{ varint.product_variant_two_display.variant_title }}/
                    </template>
                    <template v-if="varint.product_variant_three_display">
                      {{ varint.product_variant_three_display.variant_title }}
                    </template>
                  </dt>
                  <dd class="col-sm-9">
                    <dl class="row mb-0">
                      <dd class="col-sm-4 pb-0">Price : {{ varint.price }}</dd>
                      <dd class="col-sm-8 pb-0">
                        InStock : {{ varint.stock }}
                      </dd>
                    </dl>
                  </dd>
                </dl>
                <button
                  onclick="$('#variant').toggleClass('h-auto')"
                  class="btn btn-sm btn-link"
                >
                  Show more
                </button>
              </td>
              <td>
                <div class="btn-group btn-group-sm">
                  <a href="" class="btn btn-success">Edit</a>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card-footer">
      <div class="row justify-content-between">
        <div class="col-md-6">
          <p>
            Showing {{ itemStartIndex }} to {{ itemEndIndex }} out of
            {{ productCount }}
          </p>
        </div>
        <div class="col-md-6 d-flex justify-content-end mb-2">
          <b-pagination
            v-model="currentPage"
            :per-page="perPage"
            :total-rows="productCount"
            @change="fetchProductList"
          >
          </b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/",
});

export default {
  data() {
    return {
      isFiltersApplied: false,
      itemStartIndex: 0,
      itemEndIndex: 0,
      currentPage: 1,
      perPage: 2,
      search_query: "",
      productList: [],
      productCount: 0,

      variantList: [],

      productApiUrl: "api/v1/product/products/",
      variantApiUrl: "api/v1/product/variants/",

      filter_settings: {
        variant: "",
        from_price_range: "",
        to_price_range: "",
        createdDate: "",
      },
    };
  },
  created() {
    this.fetchProductList(1);
    this.fetchVarintList();
  },
  computed: {
    getVariantOptions() {
      let options = [];
      this.variantList.forEach((element) => {
        options.push({ value: element.id, text: element.title });
      });

      return options;
    },
  },
  methods: {
    fetchProductList(currentPage) {
      let relativeURL =
        this.productApiUrl + `?page_size=${this.perPage}&page=${currentPage}`;

      if (this.search_query) {
        relativeURL += `&search=${this.search_query}`;
      }
      if (this.filter_settings.variant) {
        relativeURL += `&variant=${this.filter_settings.variant}`;
      }
      if (this.filter_settings.from_price_range) {
        relativeURL += `&from_price_range=${this.filter_settings.from_price_range}`;
      }
      if (this.filter_settings.to_price_range) {
        relativeURL += `&to_price_range=${this.filter_settings.to_price_range}`;
      }
      if (this.filter_settings.createdDate) {
        relativeURL += `&created_date=${this.filter_settings.createdDate}`;
      }

      apiClient
        .get(relativeURL)
        .then((resp) => {
          this.productList = resp.data.results;
          this.productCount = resp.data.count;
          this.setItemIndex();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    fetchVarintList() {
      let relativeURL = this.variantApiUrl + `?page_size=10000&page=1`;
      apiClient
        .get(relativeURL)
        .then((resp) => {
          this.variantList = resp.data.results;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    clearFilter() {
      this.filter_settings = {
        variant: "",
        from_price_range: "",
        to_price_range: "",
        createdDate: "",
      };
      this.search_query = "";

      this.fetchProductList(1);
      this.isFiltersApplied = false;
    },

    setItemIndex() {
      this.productList.forEach((element, index) => {
        if (index == 0) {
          this.itemStartIndex = element.id;
        }

        if (index == this.productList.length - 1) {
          this.itemEndIndex = element.id;
        }
      });
    },
  },
};
</script>

<style></style>
