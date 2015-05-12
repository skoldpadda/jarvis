Code.require_file "../server/main.ex", __DIR__

ExUnit.start

defmodule EchoTest do
	use ExUnit.Case, async: true

	test "echoes message" do
		assert Echo.run("Hello world!") == "Hello world!"
	end
end
