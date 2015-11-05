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
  beforeSend: function(xhr) {
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
    debugger;
  },
  start: function() {
    $.ajax({
      url: '/api/user/logout',
      success:function() {
        setTimeout(function(){
          window.location = '/';
        }, 500);
      },
      error: function() {
        setTimeout(function(){
          window.location = '/';
        }, 500);
      }
    });
  }

});

var app = new App();


