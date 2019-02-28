/*
 * cchecker_web/static/js/app/about.js
 */

_.extend(App.prototype, {
  views: {
    navbar: null,
  },
  collections: {
  },
  models:{
    references: new ReferencesModel()
  },
  form: {},
  initializeViews: function() {
    var self = this;
    var referenceUrls = _.compact(this.models.references.get('references'));
    
    // Initialize the Navbar with a Logout button
    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      referenceUrls: referenceUrls,
      page: 'about',
    });
    this.views.navbar.render();

  }
});

