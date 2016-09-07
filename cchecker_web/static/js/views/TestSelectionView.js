/*
 * cchecker_web/static/js/views/TestSelectionView.js
 */

var TestSelectionView = Backbone.View.extend({
  initialize:function(options) {
    return this;
  },
  events:{
    'change .selectpicker' : 'onSelect'
  },
  getSelected: function() {
    return this.$el.find('.selectpicker option:selected').data('id');
  },
  setLabel: function(o) {
    var selected = this.getSelected();
    var selectedModel = this.collection.get(selected);
    var selectedDescription = selectedModel.get('description');
    this.$el.find('#test-selection-label').html('<p>' + selectedDescription + '</p>');
    return;
  },
  onSelect: function(e) {
    this.setLabel();
    e.stopPropagation();
    return;
  },
  template: JST['cchecker_web/static/js/partials/TestSelection.html'],
  render: function() {
    this.$el.html(this.template({
      collection: this.collection
    }));
    this.$el.find('.selectpicker').selectpicker();

    this.setLabel();
    return this;
  }
});
