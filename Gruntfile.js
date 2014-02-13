module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('jarvis-nw/package.json'),
        nodewebkit: {
            options: {
                version: '0.8.4',
                build_dir: './dist',
                app_name: 'jarvis',
                mac: true,
                win: true,
                linux32: true,
                linux64: true
            },
            src: './jarvis-nw/**/*'
        },
    });
    grunt.loadNpmTasks('grunt-node-webkit-builder');
    grunt.registerTask('default', ['nodewebkit']);
};