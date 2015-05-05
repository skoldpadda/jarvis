defmodule Orpheus.ClientChannel do
	use Orpheus.Web, :channel

	def join("client:echo", auth_msg, socket) do
		IO.puts "Someone's joining echo!"
		send self, %{after_join: "echo"}
		{:ok, socket}
	end

	def join("client:" <> module, auth_msg, socket) do
		:ignore
	end

	@doc """
	Swallow empty input. Ideally client implementations should handle this,
	but we do it here to reduce the chance of false positives.
	"""
	def handle_in(_, %{"data" => ""}, socket) do
		{:noreply, socket}
	end

	def handle_in("echo", message, socket) do
		push socket, "return_event", message
		{:noreply, socket}
	end

	def handle_info(%{:after_join => module}, socket) do
		push socket, "join", %{data: "Successfully joined " <> module}
		{:noreply, socket}
	end
end
