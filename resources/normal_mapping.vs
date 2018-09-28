#version 330

uniform mat4 projection_view_matrix;
uniform mat4 normal_view_matrix;

in vec4 v_pos;
in vec4 v_normal;
in vec4 v_tangent;
in vec2 uv_0;

out mat3 f_tbn;
out vec2 fuv_0;

void main()
{
    vec3 normal = (normal_view_matrix*v_normal).xyz;
    vec3 tangent = (normal_view_matrix*v_tangent).xyz;
    vec3 bitangent = cross(normal, tangent);

    f_tbn = mat3(tangent, bitangent, normal);

    fuv_0 = uv_0;
    gl_Position = projection_view_matrix*v_pos;
}