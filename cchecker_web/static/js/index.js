"use strict";
/*
 * cchecker_web/static/js/index.js
 */

var App = function() {
};

_.extend(App.prototype, {
  start: function() {
    var self = this;
    this.drop = $('#dropbox');

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

      var formData = new FormData();
      _.each(e.originalEvent.dataTransfer.files, function(file, i) {
        formData.append('file-' + i, file);
      });

      $(this).addClass('uploading');

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
        data: formData
      });
      req.always(function() {
        self.drop.removeClass('uploading');
      });
      req.done(function(data) {
        $('.drop-status').html('<div class="alert alert-success">' + data.message + '</div>');
      });
    });
  }
});

