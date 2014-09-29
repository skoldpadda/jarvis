defmodule Orpheus.ClientChannel do
	use Phoenix.Channel

	def join(socket, "echo", message) do
		IO.puts "Someone's joining echo!"
		reply socket, "join", %{content: "Joined echo successfully"}
		{:ok, socket}
	end

	def join(socket, _no, _message) do
		{:error, socket, :unauthorized}
	end

	def event(socket, "echo", message) do
		reply socket, "return_event", message
		socket
	end
end
