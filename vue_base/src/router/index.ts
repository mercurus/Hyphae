import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ViewHome from "../views/ViewHome.vue";
import ViewSearchTopic from "../views/ViewSearchTopic.vue";
import ViewSearchMorph from "../views/ViewSearchMorph.vue";
import ViewArticleTopic from "../views/ViewArticleTopic.vue";

const routes: Array<RouteRecordRaw> = [
    { path:"/", name:"home", component:ViewHome },
    { path:"/topics", name:"searchTopic", component:ViewSearchTopic },
    { path:"/topics/:id", name:"articleTopic", component:ViewArticleTopic },
    // { path:"/topics/:id", name:"articleTopic", component: ()=>import("@/views/ViewArticleTopic.vue") },
    { path:"/morphs", name:"searchMorph", component:ViewSearchMorph },
];

const router = createRouter({
    history: createWebHistory(""), //process.env.BASE_URL
    routes,
});
  // linkActiveClass: "",

export default router;
