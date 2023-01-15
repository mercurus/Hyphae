import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ViewHome from "../views/ViewHome.vue";
import ViewSearchTopic from "../views/ViewSearchTopic.vue";
import ViewSearchMorph from "../views/ViewSearchMorph.vue";
import ViewArticleTopic from "../views/ViewArticleTopic.vue";

const routes: Array<RouteRecordRaw> = [
    { path:"/", name:"home", component:ViewHome },
    { path:"/topics", name:"searchTopic", component:ViewSearchTopic },
    { 
        path:"/topics/:id", 
        name:"articleTopic", 
        component:ViewArticleTopic, 
        props: route => ({id: route.params.id})
        // props: route => ({id: parseInt(route.params.id.toString())})
    },
    
    { path:"/morphs", name:"searchMorph", component:ViewSearchMorph },
    // { path:"/morphs/:id", name:"articleMorph", component:ViewArticleMorph },
    

    // { path:"/topics/:id", name:"articleTopic", component: ()=>import("@/views/ViewArticleTopic.vue") },
];

const router = createRouter({
    history: createWebHistory(""), //process.env.BASE_URL
    routes,
});
  // linkActiveClass: "",

export default router;
