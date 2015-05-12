var gulp       = require('gulp');
var clean      = require('gulp-clean');
var less       = require('gulp-less');
var minifycss  = require('gulp-minify-css');
var uglify     = require('gulp-uglify');

var browserify = require('browserify');
var coffeeify  = require('coffeeify');
var riotify    = require('riotify');
var buffer     = require('vinyl-buffer');
var vinyl      = require('vinyl-source-stream');


var paths = {
	css: {
		src: './app/less/main.less',
		dest: '../orpheus/priv/static/css'
	},
	js: {
		src: ['./app/js/main.coffee'],
		name: 'main.js',
		dest: '../orpheus/priv/static/js'
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
	return browserify(paths.js.src)
		.transform(coffeeify)
		.transform(riotify, { type: 'coffeescript' })
		.bundle()
		.pipe(vinyl(paths.js.name))
		.pipe(buffer())
		.pipe(uglify())
		.pipe(gulp.dest(paths.js.dest));
});

gulp.task('default', ['clean'], function() {
	gulp.start('copy-assets', 'compile-css', 'compile-js');
});
