<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Router from "svelte-spa-router";
  import Write from "./pages/Write.svelte";
  import NotFound from "./NotFound.svelte";
  import "./css/style.css";

  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Signup,
    "/write": Write,
    "*": NotFound,
  };
</script>

<Router {routes} />

<style>
</style>
