#version 430 core

out vec4 colors;
out mat4 transform_final;

in vec3 frag_color;
in mat4 transform_out;



void main()
{
    colors = vec4(frag_color.rgb, 1.0f);
    transform_final = transform_out;
}