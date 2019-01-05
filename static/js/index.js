var app = new Vue({
    el: '#app',
    mixins: [utilMixin],
    data: {
        title: 'Readers Today News',
        tags: [],
        main_post: {
          media_items: [ { image: undefined}]
        },
        primary_posts: [],
        old_posts: [],
    },
    updated: function(){
      $('.cat_item')
        .dimmer({
          on: 'hover'
        })
    },
    created: function(){
      //this.get_posts()
      this.posts_updated(posts)
      this.get_tags()
    },
    computed: {
      top_tags: function(){
        return this.tags.slice(0, 6)
      }
    },
    methods: {
      posts_updated: function(all_posts){
        var vm = this
        vm.main_post = all_posts[0]
        vm.primary_posts = all_posts.slice(1, 3)
        vm.old_posts = all_posts.slice(3)
      },
      get_tags: function(){
        var vm = this
        axios.get('/api/tag/list').then(
          response=>{
            vm.tags = response.data
          },
          error=>{
            console.log(error)
          })
      },
      get_posts: function(){
        var vm = this
        axios.get('/api/post/list?limit=30').then(
        response=>{
          vm.posts_updated(response.data.results)
        },
        error=>{
          console.log(error)
        })
      },
      get_random_color_class: function(){
        var colors = ['red', 'blue', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue']
        return colors[Math.floor(Math.random() * colors.length)]
      }
    }
    })






