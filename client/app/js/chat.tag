<chat>
	<div each={ items }>
		<span class={ author.toLowerCase() }>{ author } &gt; </span><span>{ message }</span>
	</div>

	<script type="coffeescript">
		@items = []

		opts.on 'message', (message) =>
			console.log message
			@items.push message
			@update()
	</script>
</chat>
