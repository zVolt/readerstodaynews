
var menuMixin = {
    data:  function () {
        return {
            name: 'Reader\'s Today News',
            main_items: [],
            sec_items: [],
        }
    },
    created: function(){
        // create sidebar and attach to menu open
        $('.ui.sidebar').sidebar('attach events', '.toc')
        this.get_menu_items()
    },
    methods:{
        get_menu_items: function(){
            var vm = this
            axios.get('/api/menu/').then(
            response=>{
                console.log(response)
                var all_items  = response.data.results
                all_items.forEach(item => {
                    if(item.url === window.location.pathname) {
                        item.active = true
                    }
                    if (item.menu==0) {
                        vm.main_items.push(item)
                    } else {
                        vm.sec_items.push(item)
                    }
                })
            },
            error=>{
                console.log(error)
            })
        }
    }
}

var menu_main = new Vue({
    el: '#menu-main',
    mixins: [utilMixin, menuMixin],
})

var menu_fixed = new Vue({
    el: '#menu-fixed',
    mixins: [utilMixin, menuMixin],
})

var menu_sidebar = new Vue({
    el: '#menu-sidebar',
    mixins: [utilMixin, menuMixin],
})