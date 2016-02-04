"use strict"
/*
 * cchecker_web/static/js/models/ConfigModel.js
 */

var ConfigModel = Backbone.Model.extend({
  url: "/api/config",
  defaults: {
    "size_limit":0 // max size in bytes
  }
});
