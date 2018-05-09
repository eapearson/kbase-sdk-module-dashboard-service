
package us.kbase.dashboardservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.Tuple11;
import us.kbase.common.service.Tuple9;


/**
 * <p>Original spec-file type: NarrativeX</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws",
    "nar",
    "permissions"
})
public class NarrativeX {

    @JsonProperty("ws")
    private Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws;
    @JsonProperty("nar")
    private Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar;
    @JsonProperty("permissions")
    private List<UserPermission> permissions;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ws")
    public Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> getWs() {
        return ws;
    }

    @JsonProperty("ws")
    public void setWs(Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws) {
        this.ws = ws;
    }

    public NarrativeX withWs(Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws) {
        this.ws = ws;
        return this;
    }

    @JsonProperty("nar")
    public Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> getNar() {
        return nar;
    }

    @JsonProperty("nar")
    public void setNar(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar) {
        this.nar = nar;
    }

    public NarrativeX withNar(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar) {
        this.nar = nar;
        return this;
    }

    @JsonProperty("permissions")
    public List<UserPermission> getPermissions() {
        return permissions;
    }

    @JsonProperty("permissions")
    public void setPermissions(List<UserPermission> permissions) {
        this.permissions = permissions;
    }

    public NarrativeX withPermissions(List<UserPermission> permissions) {
        this.permissions = permissions;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((("NarrativeX"+" [ws=")+ ws)+", nar=")+ nar)+", permissions=")+ permissions)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
