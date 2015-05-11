defmodule Orpheus.ClientChannel do
	use Orpheus.Web, :channel

	# @TODO :ets is probably still not a viable solution (but better)
	def get_module(name) do
		case :ets.lookup(:module_registry, name) do
			[{^name, module}] -> {:ok, module}
			[] -> :module_not_found
		end
	end

	def cache_module(name) do
		case get_module(name) do
			{:ok, _} ->
				:ok
			:module_not_found ->
				# Load module in cache
				module_path = "../modules/" <> name <> "/server"
				if File.exists?(module_path <> "/main.ex") do
					loaded_module = elem(Code.load_file("main.ex", module_path) |> List.first, 0)
					if loaded_module do
						:ets.insert(:module_registry, {name, loaded_module})
					end
					:ok
				else
					:module_not_found
				end
		end
	end

	# @TODO: Check out https://github.com/bbense/pluginator
	def join("client:" <> module, auth_msg, socket) do
		IO.puts "Attempting to join " <> module
		case cache_module(module) do
			:ok ->
				send self, %{after_join: module}
				{:ok, socket}
			error ->
				{:error, socket, error}
		end
	end

	@doc """
	Swallow empty input. Ideally client implementations should handle this,
	but we do it here to reduce the chance of false positives.
	"""
	def handle_in(_, %{"data" => ""}, socket) do
		{:noreply, socket}
	end

	def handle_in(module, message, socket) do
		case get_module(module) do
			{:ok, loaded_module} ->
				push socket, "return_event", loaded_module.run(message)
			:module_not_found ->
				:ok
		end
		{:noreply, socket}
	end

	def handle_info(%{:after_join => module}, socket) do
		push socket, "join", %{data: "Successfully joined " <> module}
		{:noreply, socket}
	end
end
