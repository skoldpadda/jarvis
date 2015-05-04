defmodule Orpheus.ClientChannel do
	use Orpheus.Web, :channel

	def join("client:echo", auth_msg, socket) do
		IO.puts "Someone's joining echo!"
		send self, :after_join
		{:ok, socket}
	end

	def join("client:" <> _operation, auth_msg, socket) do
		:ignore
	end

	def handle_in("echo", %{"data" => ""}, socket) do
		{:noreply, socket}
	end

	def handle_in("echo", message, socket) do
		push socket, "return_event", message
		{:noreply, socket}
	end

	def handle_info(:after_join, socket) do
		push socket, "join", %{content: "Joined echo successfully"}
		{:noreply, socket}
	end
end
