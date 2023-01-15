<script lang="ts" setup>
    import NavbarLink from "@/components/NavbarLink.vue";
    import BIcon from "@/components/BIcon.vue";
</script>

<template>
    <nav class="navbar has-background-primary" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <NavbarLink
                :to="{name:'home'}"
                icon="sun"
                extraIconClasses="is-size-4"
            />
            <!-- Burger menu -->
            <a class="navbar-burger" role="button" aria-label="menu" aria-expanded="false">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>
        <div class="navbar-menu">
            <div class="navbar-start">
                <span class="navbar-item has-text-accent has-text-weight-bold">/</span>
                <NavbarLink
                    :to="{name:'searchTopic'}"
                    linkText="TOPICS"
                    icon="globe"
                />
                <span class="navbar-item has-text-accent has-text-weight-bold">/</span>
                <NavbarLink
                    :to="{name:'searchMorph'}"
                    linkText="MORPHS"
                    icon="puzzle-piece"
                />
            </div>
            <div class="navbar-end">
                <div class="navbar-item has-dropdown is-hoverable">
                    <a class="navbar-link has-icon-left has-background-">
                        <BIcon icon="address-card" extraClasses="is-size-4"></BIcon>
                    </a>
                    <div class="navbar-dropdown is-right has-background-primary">
                        <a class="navbar-item" href="profile">Profile</a>
                        <a class="navbar-item" href="logout">Logout</a>
                        <hr class="navbar-divider">
                        <a class="navbar-item" href="#">
                            Report an issue
                            <BIcon icon="exclamation-triangle" extra_classes="ml-2"></BIcon>
                        </a>
                    </div>
                </div>
            </div>
            <!-- <div class="navbar-end">
                <a class="navbar-item navbar-mainmenu" href="{% url 'conduct:login' %}" title="login">
                    {% icon 'far fa-address-card' %}
                </a>
            </div> -->
        </div>
    </nav>
</template>

<style type="css" scoped>
</style>