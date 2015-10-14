"use strict";
/*
 * cchecker_web/static/js/app.js
 */


var App = function() {
};

_.extend(App.prototype, Backbone.Events, {
  collections: {},
  views: {},
  models: {},
  urlRoot: $('meta[name=url-root]').attr('content'),
  initializeModels: function() {
  },

  initializeViews: function() {
  },

  initializeCollections: function() {
  },

  initializeListeners: function() {
  },

  fetchCollections: function() {
  },
  beforeSend: function(xhr, settings) {
    settings.url = this.urlRoot + settings.url.substring(1, settings.url.length);
    //xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },

  start: function() {
    this.initializeModels();
    this.initializeCollections();
    this.initializeViews();
    this.initializeListeners();
    this.fetchCollections();
  }
});

