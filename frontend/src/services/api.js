export const modernizeStream = async (fileData, onUpdate, onError) => {
  try {
    const response = await fetch("http://localhost:8000/api/modernize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // fileData: { code: "...", fileName: "...", language: "...", framework?: "..." }
      body: JSON.stringify({ 
        file_name: fileData.fileName, 
        code: fileData.code,
        language: fileData.language,
        framework: fileData.framework ?? "None",
      }),
    });

    if (!response.ok) throw new Error("Failed to connect to backend");

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n").filter((line) => line.startsWith("data: "));

      lines.forEach((line) => {
        try {
          const payload = JSON.parse(line.replace("data: ", ""));
          if (payload.error) onError(payload.error);
          else onUpdate(payload);
        } catch (e) {
          console.error("Error parsing JSON chunk", e);
        }
      });
    }
  } catch (err) {
    onError(err.message);
  }
};