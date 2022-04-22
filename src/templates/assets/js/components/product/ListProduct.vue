<template>
  <div class="card">
    <form action="" method="get" class="card-header">
      <div class="form-row justify-content-between">
        <div class="col-md-2">
          <input
            type="text"
            name="title"
            placeholder="Product Title"
            class="form-control"
          />
        </div>
        <div class="col-md-2">
          <select name="variant" id="" class="form-control">
            <option selected disabled>--Select A Variant--</option>
          </select>
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
            />
            <input
              type="text"
              name="price_to"
              aria-label="Last name"
              placeholder="To"
              class="form-control"
            />
          </div>
        </div>
        <div class="col-md-2">
          <input
            type="date"
            name="date"
            placeholder="Date"
            class="form-control"
          />
        </div>
        <div class="col-md-1">
          <button type="submit" class="btn btn-primary float-right">
            <i class="fa fa-search"></i>
          </button>
        </div>
      </div>
    </form>

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
          <p>Showing 1 to 10 out of 100</p>
        </div>
        <div class="col-md-2"></div>
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
      currentPage: 1,
      perPage: 3,
      search_query: "",
      productList: [],
      productCount: 0,
      productApiUrl: "api/v1/product/products/",

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
  },
  methods: {
    fetchProductList(currentPage) {
      let relativeURL =
        this.productApiUrl + `?page_size=${this.perPage}&page=${currentPage}`;

      console.log(relativeURL);

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
          console.log(resp);
          this.productList = resp.data.results;
          this.productCount = resp.data.count;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
