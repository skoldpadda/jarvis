var gulp       = require('gulp');
var clean      = require('gulp-clean');
var concat     = require('gulp-concat');
var less       = require('gulp-less');
var minifycss  = require('gulp-minify-css');
var uglify     = require('gulp-uglify');

var paths = {
	css: {
		src: './app/less/main.less',
		dest: '../orpheus/priv/static/css'
	},
	js: {
		src: ['./app/js/app.js'],
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
	return gulp.src(paths.js.src)
		.pipe(concat(paths.js.name))
		.pipe(uglify())
		.pipe(gulp.dest(paths.js.dest));
});

gulp.task('default', ['clean'], function() {
	gulp.start('copy-assets', 'compile-css', 'compile-js');
});
