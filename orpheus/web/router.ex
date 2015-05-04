defmodule Orpheus.Router do
  use Orpheus.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", Orpheus do
    pipe_through :browser # Use the default browser stack

    get "/", PageController, :index
  end

  # Other scopes may use custom stacks.
  # scope "/api", Orpheus do
  #   pipe_through :api
  # end

  socket "/kernel", Orpheus do
    channel "client:*", ClientChannel
  end
end
