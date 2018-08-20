from os import path

from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_loader import ResourceLoader
from gcraft.resources.resource_types import RT_SHADER_PROGRAM


class DefaultShaderLoader(ResourceLoader):

    def __init__(self):
        pass

    def can_load(self, r_id, r_type):
        return r_type == RT_SHADER_PROGRAM and (r_id == "default_basic" or r_id == "default_lighting")

    def load(self, r_id) -> Resource:
        if r_id == "default_basic":
            return Shader(r_id, """
                    #version 330
                    uniform mat4 projection_view_matrix;

                    in vec4 v_pos;
                    in vec2 uv_0;

                    out vec2 fuv_0;

                    void main() 
                    {  
                        fuv_0 = uv_0;
                        gl_Position = projection_view_matrix*v_pos;   
                    }
                """,
                """
                    #version 330
                    uniform vec4 difusse_color;
                    uniform int textures_count;
                    uniform sampler2D texture_0;

                    in vec2 fuv_0;

                    out vec4 frag_color;

                    void main() 
                    {   
                        if(textures_count == 0)
                            frag_color = difusse_color;
                        else if(textures_count == 1)
                            frag_color = texture2D(texture_0, fuv_0) *difusse_color; 
                    }
                """)

        elif r_id == "default_lighting":
            return Shader(r_id, """
                    #version 330
                    uniform vec3 light_dir;
                    uniform mat4 projection_view_matrix;
                    uniform mat4 normal_view_matrix;

                    in vec4 v_pos;
                    in vec4 v_normal;
                    in vec2 uv_0;

                    out vec2 fuv_0;
                    out float flight;

                    void main() 
                    {   
                        vec3 t_normal = (normal_view_matrix*v_normal).xyz;
                        flight = clamp(dot(t_normal, normalize(light_dir)*-1), 0.0, 1.0);

                        fuv_0 = uv_0;
                        gl_Position = projection_view_matrix*v_pos;   
                    }
                """,
                """
                    #version 330
                    uniform float ambient_lighting;
                    uniform vec4 difusse_color;
                    uniform int textures_count;
          
                    uniform sampler2D texture_0;
          
                    in vec2 fuv_0;
                    in float flight;
                    out vec4 frag_color;
          
                    void main() 
                    {   
                        vec4 final_diffuse = difusse_color;
          
                        if(textures_count > 0)
                            final_diffuse *= texture2D(texture_0, fuv_0);
          
                        vec4 ambient_color = final_diffuse*ambient_lighting;
                        frag_color = clamp(ambient_color + final_diffuse*flight, 0.0, 1.0);
                    }
                """)
        return None


class FileShaderLoader(ResourceLoader):

    def __init__(self):
        pass

    def can_load(self, r_id, r_type):
        if r_type != RT_SHADER_PROGRAM or not isinstance(r_id, tuple) or len(r_id) != 2:
            return False
        if not r_id[0].endswith(".vs") or not r_id[1].endswith(".fs"):
            return False
        if not path.exists(r_id[0]) or not path.exists(r_id[1]):
            return False

        return True

    def load(self, r_id) -> Resource:
        return Shader(r_id,
                      open(r_id[0], 'r').read(),
                      open(r_id[1], 'r').read())
