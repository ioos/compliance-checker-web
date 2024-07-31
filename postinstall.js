const fs = require('fs');
const path = require('path');

const modules = [
  'backbone',
  'backbone.stickit',
  'bootstrap',
  'bootstrap-select',
  'font-awesome',
  'jquery',
  'moment',
  'underscore'
];

const libDir = path.resolve('cchecker_web/static/lib');

// Ensure the lib directory exists
if (!fs.existsSync(libDir)) {
  fs.mkdirSync(libDir, { recursive: true });
}

modules.forEach(module => {
  const target = path.resolve('node_modules', module);
  const link = path.resolve(libDir, module);
  
  try {
    if (fs.existsSync(link)) {
      console.log(`Symlink for ${module} already exists.`);
    } else {
      fs.symlinkSync(target, link, 'junction');
      console.log(`Symlink created for ${module}`);
    }
  } catch (e) {
    console.error(`Failed to symlink ${module}: ${e.message}`);
  }
});

