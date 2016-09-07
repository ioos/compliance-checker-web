/*
 * cchecker_web/static/js/views/IOOSNavbarView.js
 * Navbar with the IOOS theme
 */

var IOOSNavbarView = BaseView.extend({
  initialize:function(options) {
    this.options = _.extend({
      links: [],
      referenceUrls: [],
    }, options);

    BaseView.prototype.initialize.call(this);
  },
  templateName: "IOOSNavbar",
  render: function() {
    var self = this;
    this.$el.html(this.template({links: this.options.links,
                                 referenceUrls: this.options.referenceUrls}));
    return this;
  }
});
