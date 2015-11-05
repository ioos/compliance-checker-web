"use strict"
/*
 * cchecker_web/static/js/views/UserPasswordResetFormView.js
 */

var UserPasswordResetFormView = Backbone.View.extend({
  bindings: {
    '#email' : 'email'
  },
  events: {
    'click #reset': 'onReset'
  },
  onReset: function(e) {
    e.preventDefault();
    this.trigger('passwordReset', this.model);
  },
  initialize: function(options) {
    this.options = _.extend({
      legend: "Reset my password"
    }, options);
  },
  template: JST['cchecker_web/static/js/partials/UserPasswordResetForm.html'],
  render: function() {
    this.$el.html(this.template({legend: this.options.legend}));
    this.stickit();
    return this;
  }
});
