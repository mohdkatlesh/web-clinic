$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/covid',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' The Chest x-Ray image from class ' + data);
                console.log('Success!');
            },
        });
    });

});


// for animated background
((c) => {
    const options = {
        num: 40,
        particle: {color: 'rgba(0, 0, 0, 0.6)',
                   szMin: 0.5, szMax: 1,
                   spMin: 0.05, spMax: 0.5},
        link: {color: 'rgba(0, 0, 0, 0.6)', maxDist: 120}
    };

    const pi2  = Math.PI*2;
    const degrad = Math.PI / 180.0;
    const ctx = c.getContext('2d');
    let w = c.width = window.innerWidth;
    let h = c.height = window.innerHeight;

    class Particle {
        constructor() {
            this.p = {x: Math.random() * c.width, y: Math.random() * c.height};
            this.s = options.particle.spMin + Math.random() * options.particle.spMax;
            this.r = options.particle.szMin + Math.random() * options.particle.szMax;
            this.d = Math.random() * pi2;
            this.v = {x: Math.cos(this.d) * this.s, y: Math.sin(this.d) * this.s};
        }
        setDir(d) {
            this.d = d;
            this.v.x = Math.cos(this.d) * this.s;
            this.v.y = Math.sin(this.d) * this.s;
        }
        wrap() {
            if(this.p.x < 0 || this.p.x > w || this.p.y < 0 || this.p.y > h)
                this.setDir(this.d + Math.random() * degrad * 5);
            if( this.p.x < 0) this.p.x += w;
            if( this.p.x > w) this.p.x -= w;
            if( this.p.y < 0) this.p.y += h;
            if( this.p.y > h) this.p.y -= h;
        }
        update() {
            this.p.x += this.v.x;
            this.p.y += this.v.y;
            this.wrap();
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.p.x, this.p.y, this.r, 0, pi2);
            ctx.fillStyle = options.particle.color;
            ctx.fill();
        }
        drawLink(other) {
            ctx.save();
            ctx.globalAlpha = 1 - (this.distanceTo(other) / options.link.maxDist);
            ctx.beginPath();
            ctx.moveTo(this.p.x, this.p.y);
            ctx.lineWidth = this.r;
            ctx.lineTo(other.p.x, other.p.y);
            ctx.strokeStyle = options.link.color;
            ctx.stroke();
            ctx.restore();
        }
        closeTo(other) {
            let xd = other.p.x - this.p.x;
            let yd = other.p.y - this.p.y;

            return (xd*xd + yd*yd) <= (options.link.maxDist * options.link.maxDist);
        }
        distanceTo(other) {
            let xd = other.p.x - this.p.x;
            let yd = other.p.y - this.p.y;
            
            return Math.sqrt(xd*xd + yd*yd);
        }
    }

    const particles = [...Array(options.num)].map((_, i) => new Particle);

    const resize = () => {
        let s = {x: window.innerWidth / w, y: window.innerHeight / h};
        w = c.width = window.innerWidth;
        h = c.height = window.innerHeight;
        particles.forEach((particle) => {
            particle.p.x *= s.x;
            particle.p.y *= s.y;
            particle.draw();
        });
    };

    let integrate = () => {
        ctx.clearRect(0, 0, w, h);
        particles.forEach((a) => {
            a.update();
            a.draw();
            particles.forEach((b) => {
                if( a === b || !b.closeTo(a) ) return;
                a.drawLink(b);
            });

        });
        window.requestAnimationFrame(integrate);
    };

    const init = () => {
        c.classList.add('network-background-canvas');
        document.body.insertAdjacentElement('beforeend', c);
        resize();
        window.addEventListener('resize', resize);
        window.requestAnimationFrame(integrate);
    };

    document.addEventListener('DOMContentLoaded', init);
})(document.createElement('canvas'));
