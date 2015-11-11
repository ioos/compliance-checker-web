"use strict"
/*
 * cchecker_web/static/js/app/NewUser.js
 */

_.extend(App.prototype, {
  models: {
  },
  views: {
    navbar: null,
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
    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      links: []
    });
    this.views.navbar.render();

    this.views.userTableView = new UserTableView({
      collection: this.collections.userCollection,
      el: $('#user-table-view')
    });
  },
  initializeCollections: function() {
    var self = this;
    $.when(this.collections.userCollection.fetch({
      beforeSend: self.beforeSend.bind(self)
    })).done(function() {
      self.views.userTableView.render();
    });
  },
  initializeListeners: function() {
    var self = this;
  },
  fetchCollections: function() {
    var self = this;
  },
  beforeSend: function(xhr, settings) {
    settings.url = this.urlRoot + settings.url.substring(1, settings.url.length);
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  test: function() {
    var self = this;
  }
});

var app = new App();


