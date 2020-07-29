// Managing text oveflow in the posts list
document.addEventListener( "DOMContentLoaded", () => {
   let wrapper = document.querySelector( ".content" );
   let options = {
      ellipsis: "\u2026 ",
   };
   new Dotdotdot( wrapper, options );
});