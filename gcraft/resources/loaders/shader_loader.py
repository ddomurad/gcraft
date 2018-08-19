from gcraft.resources.resource import Resource
from gcraft.resources.shader import Shader
from gcraft.resources.resource_loader import ResourceLoader
from gcraft.resources.resource_types import RT_SHADER_PROGRAM


class DefaultShaderLoader(ResourceLoader):

    def __init__(self):
        pass

    def can_load(self, r_id, r_type):
        return r_type == RT_SHADER_PROGRAM and (r_id == "default_basic" or r_id == "default_lighting"
                                                or r_id == "default_normal_mapping")

    def load(self, r_id) -> Resource:
        if r_id == "default_basic":
            return Shader(r_id, """#version 330

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
                          """#version 330
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
            return Shader(r_id, """#version 330
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
                          """#version 330
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

        elif r_id == "default_normal_mapping":
            return Shader(r_id, """#version 330
                    uniform mat4 projection_view_matrix;
                    uniform mat4 normal_view_matrix;

                    in vec4 v_pos;
                    in vec4 v_normal;
                    in vec4 v_tangent;
                    in vec2 uv_0;

                    out vec3 f_normal;
                    out vec3 f_tangent;
                    out vec3 f_bitangent;

                    out vec2 fuv_0;

                    void main() 
                    {   
                        f_normal = (normal_view_matrix*v_normal).xyz;
                        f_tangent = (normal_view_matrix*v_tangent).xyz;
                        f_bitangent = cross(f_normal, f_tangent);

                        fuv_0 = uv_0;
                        gl_Position = projection_view_matrix*v_pos;   
                    }
                """,
                          """#version 330
                              uniform vec3 light_dir;
                              uniform float ambient_lighting;
                              uniform vec4 difusse_color;
                              uniform int textures_count;

                              uniform sampler2D texture_0;
                              uniform sampler2D texture_1;

                              in vec3 f_normal;
                              in vec3 f_tangent;
                              in vec3 f_bitangent;

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
                                      vec3 p_normal = 2.0*texture2D(texture_1, fuv_0).xyz - 1.0;
                                      mat3 tbm = mat3(f_bitangent, f_tangent, f_normal);

                                      vec3 new_normal = tbm*p_normal;
                                      flight = clamp(dot(new_normal, normalize(light_dir)*-1), 0.0, 1.0);
                                  }
                                    //  final_diffuse = (texture2D(texture[0], fuv_0)/2.0  + texture2D(texture[1], fuv_0)/2.0) *difusse_color;

                                  vec4 ambient_color = final_diffuse*ambient_lighting;
                                  frag_color = clamp(ambient_color + final_diffuse*flight, 0.0, 1.0);
                              }
                          """)
        return None
