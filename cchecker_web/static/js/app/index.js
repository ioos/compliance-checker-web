"use strict";
/*
 * cchecker_web/static/js/app/index.js
 */

_.extend(App.prototype, {
  views: {
    testSelection: null
  },
  collections: {
    testCollection: new TestCollection()
  },
  form: new FormData(),
  initializeViews: function() {
    var self = this;
    this.views.testSelection = new TestSelectionView({
      el: $('.testselection'),
      collection: this.collections.testCollection
    });
  },
  initializeCollections: function() {
    var self = this;
    var testFetch = this.collections.testCollection.fetch();
    $.when.apply($, [testFetch]).done(function() {
      self.views.testSelection.render();
    });
  },
  start: function() {
    var self = this;
    this.drop = $('#dropbox');
    this.submit = $('#submit-btn');

    this.drop.on('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
    });

    this.drop.on('dragenter', function(e) {
      $(this).addClass('hovered');
    });

    this.drop.on('dragleave', function(e) {
      $(this).removeClass('hovered');
    });

    this.drop.on('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();

      _.each(e.originalEvent.dataTransfer.files, function(file, i) {
        self.form.append('file-' + i, file);
      });

      $(this).addClass('uploading');
    });
    this.submit.on('click', function() {
      var urlInput = $('#url-input').val();
      if(urlInput.length > 0) {
        self.form.append('url', urlInput);
      }
      var req = $.ajax({
        url: '/upload',
        xhr: function() {
          var x = $.ajaxSettings.xhr();
          x.upload.addEventListener('progress', function(e) {
            if(e.lengthComputable) {
              var pct = e.loaded / e.total * 100;
              console.log(pct);
            }
          }, false);
          return x;
        },
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        data: self.form
      });
      req.always(function() {
        self.drop.removeClass('uploading');
      });
      req.done(function(data) {
        $('.drop-status').html('<div class="alert alert-success">' + data.message + '</div>');
        self.pollResult(data.job_id);
      });
    });
    this.initializeModels();
    this.initializeCollections();
    this.initializeViews();
    this.initializeListeners();
    this.fetchCollections();
    this.test();
  },
  pollResult: function(jobID) {
    var self = this;
    $.ajax({
      url: '/api/job/' + jobID,
      dataType: 'json',
      method: 'GET',
      beforeSend: this.beforeSend.bind(this),
      success: function() {
        console.log("Fetch successful");
        window.location.href = self.urlRoot + 'report/' + jobID;
      },
      error: function() {
        setTimeout(function() {
          self.pollResult(jobID)
        }, 500);
      }
    });
  },
  beforeSend: function(xhr, settings) {
    settings.url = this.urlRoot + settings.url.substring(1, settings.url.length);
    //xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  test: function() {
    this.collections.tests = new TestCollection();
    this.collections.tests.fetch();
  }
});

