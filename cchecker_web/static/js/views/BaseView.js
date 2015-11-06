/*
 * cchecker_web/static/js/views/BaseView.js
 */

var BaseView = Backbone.View.extend({
  initialize: function(options) {
    if(this.templateName) {
      var pathName = 'cchecker_web/static/js/partials/' + this.templateName + '.html'
      this.template = JST[pathName];
    }
  },
  render: function() {
    this.$el.html(this.template());
    return this;
  }
});
