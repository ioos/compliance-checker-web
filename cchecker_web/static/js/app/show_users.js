"use strict"
/*
 * cchecker_web/static/js/app/NewUser.js
 */

_.extend(App.prototype, {
  models: {
  },
  views: {
    userTableView: null
  },
  collections: {
    userCollection: new UserCollection()
  },
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  initializeModels: function() {
    var self = this;
  },
  initializeViews: function() {
    var self = this;

    this.views.userTableView = new UserTableView({
      collection: this.collections.userCollection,
      el: $('#user-table-view')
    });
  },
  initializeCollections: function() {
    var self = this;
    $.when(this.collections.userCollection.fetch()).done(function() {
      self.views.userTableView.render();
    });
  },
  initializeListeners: function() {
    var self = this;
  },
  fetchCollections: function() {
    var self = this;
  },
  beforeSend: function(xhr) {
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  test: function() {
    var self = this;
  }
});

var app = new App();


