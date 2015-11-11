"use strict"
/*
 * cchecker_web/static/js/app/EditUser.js
 */

_.extend(App.prototype, {
  models: {
  },
  views: {
  },
  collections: {},
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  beforeSend: function(xhr, settings) {
    settings.url = this.urlRoot + settings.url.substring(1, settings.url.length);
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  initializeViews: function() {
    var self = this;

    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      links: []
    });
    this.views.navbar.render();
  },
  fetchCollections: function() {
    var self = this;
    $.ajax({
      beforeSend: this.beforeSend.bind(this),
      url: '/api/user/logout',
      success:function() {
        setTimeout(function(){
          window.location = app.urlRoot;
        }, 500);
      },
      error: function() {
        setTimeout(function(){
          window.location = app.urlRoot;
        }, 500);
      }
    });
  }

});

var app = new App();


