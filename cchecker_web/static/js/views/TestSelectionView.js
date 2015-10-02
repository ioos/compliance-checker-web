/*
 * cchecker_web/static/js/views/TestSelectionView.js
 */

var TestSelectionView = Backbone.View.extend({
  initialize:function(options) {
    return this;
  },
  template: JST['cchecker_web/static/js/partials/TestSelection.html'],
  render: function() {
    this.$el.html(this.template({collection: this.collection}));
    this.$el.find('.selectpicker').selectpicker();
    return this;
  }
});
