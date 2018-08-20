#version 330

uniform vec3 light_dir;
uniform float ambient_lighting;
uniform vec4 difusse_color;
uniform int textures_count;

uniform sampler2D texture_0;
uniform sampler2D texture_1;

in mat3 f_tbn;

in vec2 fuv_0;
out vec4 frag_color;

void main()
{
    vec4 final_diffuse = difusse_color;

    if(textures_count > 0)
        final_diffuse *= texture2D(texture_0, fuv_0);

    float flight = 1.0;

    if(textures_count > 1)
    {
        vec3 normal_map_val = texture2D(texture_1, fuv_0).xyz;
        normal_map_val.x = 1 - normal_map_val.x;
        normal_map_val.y = 1 - normal_map_val.y;

        vec3 p_normal = normalize(2.0*(normal_map_val) - 1.0);

        vec3 new_normal = normalize(f_tbn*p_normal);
        flight = clamp(dot(new_normal, normalize(light_dir)*-1), 0.0, 1.0);
    }

    vec4 ambient_color = final_diffuse*ambient_lighting;
    frag_color = clamp(ambient_color + final_diffuse*flight, 0.0, 1.0);
}