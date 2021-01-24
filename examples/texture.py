import glnext
from glnext_compiler import glsl
from PIL import Image

instance = glnext.instance()

texture = Image.open('examples/rock.jpg').convert('RGBA')
image = instance.image(texture.size, '4b')
image.write(texture.tobytes())

sampler = instance.sampler(image)

renderer = instance.render_set((512, 512))

pipeline = renderer.pipeline(
    vertex_shader=glsl('''
        #version 450
        #pragma shader_stage(vertex)

        layout (location = 0) in vec2 in_vert;
        layout (location = 1) in vec2 in_text;

        layout (location = 0) out vec2 out_text;

        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            out_text = in_text;
        }
    '''),
    fragment_shader=glsl('''
        #version 450
        #pragma shader_stage(fragment)

        layout (binding = 1) uniform sampler2D Texture[];

        layout (location = 0) in vec2 in_text;
        layout (location = 0) out vec4 out_color;

        void main() {
            out_color = texture(Texture[0], in_text);
        }
    '''),
    vertex_format='2f 2f',
    vertex_count=3,
    samplers=[sampler],
)

pipeline.update(
    vertex_buffer=glnext.pack([
        -0.5, -0.5, 0.0, 0.0,
        0.5, -0.5, 1.0, 0.0,
        0.0, 0.5, 0.5, 1.0,
    ]),
)

instance.render()
data = renderer.output[0].read()
Image.frombuffer('RGB', (512, 512), data, 'raw', 'BGRX', 0, -1).show()
