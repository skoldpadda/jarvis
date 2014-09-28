var gulp       = require('gulp');
var clean      = require('gulp-clean');
var less       = require('gulp-less');
var minifycss  = require('gulp-minify-css');
var uglify     = require('gulp-uglify');

var paths = {
	css: {
		src: './app/less/main.less',
		dest: '../orpheus/priv/static/css'
	},
	assets: {
		list: ['./app/img/**/*.*'],
		base: './app',
		dest: '../orpheus/priv/static'
	}
};

gulp.task('clean', function() {
	/*return gulp.src(paths.dist, {read: false})
		.pipe(clean());*/
});

gulp.task('copy-assets', function() {
	return gulp.src(paths.assets.list, {base: paths.assets.base})
		.pipe(gulp.dest(paths.assets.dest));
});

gulp.task('compile-css', function() {
	return gulp.src(paths.css.src)
		.pipe(less())
		.pipe(minifycss())
		.pipe(gulp.dest(paths.css.dest));
});

gulp.task('compile-js', function() {
	// @TODO: Figure out how to go about doing this
});

gulp.task('default', ['clean'], function() {
	gulp.start('copy-assets', 'compile-css', 'compile-js');
});
