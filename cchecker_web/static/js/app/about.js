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
  },
  form: {},
  initializeViews: function() {
    var self = this;
    var referenceUrls = _.compact([
        {
          href:  'http://wiki.esipfed.org/index.php/Category:Attribute_Conventions_Dataset_Discovery',
          title: 'ACDD wiki',
          text:  'ACDD',
        },
        {
          href:  'http://cfconventions.org/documents.html',
          title: 'CF Conventions',
          text:  'CF Conventions',
        },
        {
          href:  'https://github.com/ioos/ioosngdac/wiki/NGDAC-NetCDF-File-Format-Version-2',
          title: 'NGDAC NetCDF File Format Version 2',
          text:  'Glider DAC wiki',
        },
        {
          href:  'https://www.nodc.noaa.gov/data/formats/netcdf/v2.0/',
          title: 'NCEI NetCDF Templates v2.0',
          text:  'NCEI NetCDF Templates v2.0',
        },
        {
          href:  'http://data.nodc.noaa.gov/thredds/catalog/testdata/mbiddle/GOLD_STANDARD_NETCDF/catalog.html',
          title: 'NCEI Gold Standard Example',
          text:  'NCEI Example',
        },
        {
          href:  'https://ioos.github.io/ioos-netcdf/ioos-netcdf-metadata-description-v1-1.html#ioos-netcdf-metadata-profile-attributes',
          title: 'IOOS NetCDF v1.1 Standard',
          text:  'IOOS NetCDF',
        }
    ]);
    // Initialize the Navbar with a Logout button
    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      referenceUrls: referenceUrls,
      page: 'about',
    });
    this.views.navbar.render();

  }
});

