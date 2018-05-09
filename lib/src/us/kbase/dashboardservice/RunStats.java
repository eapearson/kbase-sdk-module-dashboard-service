
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
import us.kbase.common.service.Tuple2;


/**
 * <p>Original spec-file type: RunStats</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "timings"
})
public class RunStats {

    @JsonProperty("timings")
    private List<Tuple2 <String, Long>> timings;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("timings")
    public List<Tuple2 <String, Long>> getTimings() {
        return timings;
    }

    @JsonProperty("timings")
    public void setTimings(List<Tuple2 <String, Long>> timings) {
        this.timings = timings;
    }

    public RunStats withTimings(List<Tuple2 <String, Long>> timings) {
        this.timings = timings;
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
        return ((((("RunStats"+" [timings=")+ timings)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
