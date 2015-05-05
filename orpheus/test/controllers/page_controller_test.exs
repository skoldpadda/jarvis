defmodule Orpheus.PageControllerTest do
	use Orpheus.ConnCase, async: true

	test "GET /" do
		conn = get conn(), "/"
		assert html_response(conn, 200) =~ "<title>jarvis</title>"
	end
end
