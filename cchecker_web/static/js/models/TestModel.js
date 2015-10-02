/*
 * cchecker_web/static/js/models/TestModel.js
 */

var TestModel = Backbone.Model.extend({
  defaults: {
    name: "",
    version: ""
  }
});

var TestCollection = Backbone.Collection.extend({
  url: "/json/tests.json"
});
