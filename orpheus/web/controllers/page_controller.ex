defmodule Orpheus.PageController do
  use Orpheus.Web, :controller

  plug :action

  def index(conn, _params) do
    render conn, "index.html"
  end
end
